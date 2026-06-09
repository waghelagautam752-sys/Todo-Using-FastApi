from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel


app=FastAPI()

tasks =[]
nextid=1
class Create_task_in(BaseModel):
    #Id:int
    Title:str
    secret_code:str

class Create_task_out(BaseModel):
    Id:int
    Title:str
    Completed:bool = False

    """
    Without tags:
    GET /users/
    POST /users/
    GET /items/
    POST /items/

    With tags:
    ▼ users
    GET /users/
    POST /users/

    ▼ items
    GET /items/
    POST /items/
    """

@app.post("/Create_task/", tags=["Creating task"],response_model=Create_task_out)
async def create_task(task:Create_task_in):
    global nextid

    new_task={
        "Id":nextid,
        "Title":task.Title,
        "Completed":False
    }
    tasks.append(new_task)
    nextid+=1

    return new_task

@app.get("/Gettask",tags=["Get task"],response_model=list[Create_task_out])
async def get_task():
    return tasks

@app.get("/gettask/{task_id}",tags=["Get task"],response_model=Create_task_out)
async def gettast(task_id:int):
    for task in tasks:
        if task["Id"]==task_id:
            return task
                                    #Resource not found
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail="Task Not Found")

@app.delete("/deletetask/{task_id}",tags=["Delete Task"])
async def del_task(task_id:int):
    for task in tasks:
        if task["Id"]==task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
                                #Resource not found    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail="Task Not Found")

@app.patch("/task/{task_id}/completed" ,tags=["Status"])
async def complete_task(task_id:int):
    for task in tasks:
        if task["Id"]==task_id:
            task["Completed"]=True
            return task
                                    #Resource not found 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task Not Found")

#Fetching title by path parameter
#@app.get("/title")


@app.get("/Search_task/",tags=["Search Task"])
async def read_items(q: str | None = None):
    for task in tasks:
        if task["Title"]==q:
            return {"Message":f"Title: {task['Title']} exists"}
                                    #Resource not found 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task Not Found", headers={"X-Error": "There goes my error"},)
        

#Replacing the Entire Task except Id and secret code

class put_update_task(BaseModel):
    Title:str
    Completed:bool

@app.put("/task/{task_id}")
async def put_task(task_id:int,put_task:put_update_task):
    for task in tasks:
        if task["Id"]==task_id:
            task["Title"]=put_task.Title
            task["Completed"]=put_task.Completed
            return task
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found", headers={"X-Error": "There goes my error"},)