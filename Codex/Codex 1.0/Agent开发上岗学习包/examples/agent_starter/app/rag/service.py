from dataclasses import dataclass
@dataclass(frozen=True)
class Chunk:
    chunk_id:str; tenant_id:str; text:str; source:str
class RagService:
    def __init__(self,chunks:list[Chunk]): self.chunks=chunks
    def search(self,query:str,tenant_id:str,top_k:int=5)->list[Chunk]:
        terms=set(query.lower().split())
        scored=[]
        for c in self.chunks:
            if c.tenant_id!=tenant_id: continue
            score=sum(1 for t in terms if t in c.text.lower())
            if score: scored.append((score,c))
        scored.sort(key=lambda x:x[0],reverse=True)
        return [c for _,c in scored[:top_k]]
