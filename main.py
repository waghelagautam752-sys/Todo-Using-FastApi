from fastapi import FastAPI,HTTPException
from pydantic import BaseModel


app=FastAPI()

tasks =[]
nextid=1
class Create_task(BaseModel):
    #Id:int
    Title:str
    Status:bool=False

@app.post("/Create_task/")
async def create_task(task:Create_task):
    global nextid

    new_task={
        "Id":nextid,
        "Title":task.Title,
        "Completed":task.Status
    }
    tasks.append(new_task)
    nextid+=1

    return new_task

@app.get("/Gettask")
async def get_task():
    return tasks

@app.get("/gettask/{task_id}")
async def gettast(task_id:int):
    for task in tasks:
        if task["Id"]==task_id:
            return task
    
    raise HTTPException(status_code=404 ,detail="Task Not Found")

@app.delete("/deletetask/{task_id}")
async def del_task(task_id:int):
    for task in tasks:
        if task["Id"]==task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404 ,detail="Task Not Found")

@app.patch("/task/{task_id}/completed")
async def complete_task(task_id:int):
    for task in tasks:
        task["Id"]==task_id
        task["Completed"]=True
        return task

    raise HTTPException(status_code=404, detail="Task Not Found")

#Fetching title by path parameter
#@app.get("/title")


@app.get("/Search_task/")
async def read_items(q: str | None = None):
    for task in tasks:
        if task["Title"]==q:
            return {"Message":f"Title: {task['Title']} exists"}
    raise HTTPException(status_code=404, detail="Task Not Found", headers={"X-Error": "There goes my error"},)
        