import uvicorn;
from fastapi import FastAPI, HTTPException;
from fastapi.middleware.cors import CORSMiddleware;


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
# app.include_router(test.router)/
# app.include_router(secure_routes.router)
# app.include_router(secure_routes.router)


# if __name__=="__main__":
#      uvicorn.run(app,host="0.0.0.0",port=3002)