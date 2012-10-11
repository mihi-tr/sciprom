from Bio import Entrez

class Pubmed:
  def __init__(self,email):
    Entrez.email=email

  def query(self,str):
    handle=Entrez.esearch("pubmed",str)
    record=Entrez.read(handle)
    handle.close()
    self.querystr=str
    self.ids=record["IdList"]
  
  def fetch(self):
    handle=Entrez.efetch("pubmed",id=",".join(self.ids),retmode="xml")
    self.records=[i for i in Entrez.parse(handle)]
    handle.close()

  def parse(self):
    self.articles=[self.parse_record(i) for i in self.records]
    
  def parse_record(self,record):
    pmid=str(record["MedlineCitation"]["PMID"])
    authors=[dict(i) for i in
      record["MedlineCitation"]["Article"]["AuthorList"]]
    return {"PMID":pmid, "authors":authors} 
  
