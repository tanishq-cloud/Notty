import uvicorn;
from fastapi import FastAPI, HTTPException;
from fastapi.middleware.cors import CORSMiddleware;


from db.database import create_table
from routes import note, user

app= FastAPI()

origins =[
     
    #  "http:localhost:3000"
     '*'
]

app.add_middleware(
     CORSMiddleware,
     allow_origins=origins,
     allow_credentials=True,
     allow_methods=['*'],
     allow_headers=['*']

)
@app.on_event("startup")
async def start_up_event():
    create_table()
app.include_router(note.router)
app.include_router(user.router)

# app.include_router(secure_routes.router)
# app.include_router(secure_routes.router)


