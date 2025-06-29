from fastapi import FastAPI, Request, HTTPException
import uvicorn
from pydantic import BaseModel

application = FastAPI()

@application.get("/")
def status(request: Request):
    bot = request.app.state.bot
    return {
        "Nome": bot.user.name,
        "ID": bot.user.id,
        "Servidores": f"{len(bot.guilds)}",
        "Usuários": f"{len(set(bot.get_all_members()))}",
        "Latência": f"{round(bot.latency * 1000)}ms"
    }

# Seção: API REST

class Item(BaseModel):
    name: str
    id: int
    servers: int
    members: int
    latency: int

items = {}

# GET

@application.get("/items")
def get_items():
    return items

# POST

@application.post("/create")
def post_item(item: Item):
    if item.id in items:
        raise HTTPException(status_code=400, detail="Item com esse ID já existe!")
    items[item.id] = item.dict()
    return {"Mensagem": "item criado!", "item": item}

# PUT

@application.put("/update")
def put_item(item: Item):
    if item.id not in items:
        raise HTTPException(status_code=404, detail="Item com esse ID não existe!")
    items[item.id] = item.dict()
    return {"Mensagem": "item atualizado!", "item": item}

# DELETE

@application.delete("/delete")
def delete_item(item: Item):
    if item.id not in items:
        raise HTTPException(status_code=404, detail="Item com esse ID não existe!")
    deleted = items.pop(item.id)
    return {"Mensagem": "item deletado!", "item": deleted}