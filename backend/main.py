from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Resource(BaseModel):
    type: str
    name: str
    properties: Dict[str, str]

class InfraRequest(BaseModel):
    resources: List[Resource]

@app.post("/generate-terraform/")
def generate_terraform(data: InfraRequest):
    tf_code = ""
    for res in data.resources:
        if res.type == "ec2":
            tf_code += f'resource "aws_instance" "{res.name}" {{\n'
            tf_code += f'  ami = "ami-123456"\n'
            tf_code += f'  instance_type = "{res.properties.get("instance_type", "t2.micro")}"\n'
            tf_code += '}\n\n'
        elif res.type == "s3":
            tf_code += f'resource "aws_s3_bucket" "{res.name}" {{\n'
            tf_code += f'  bucket = "{res.name}"\n'
            if res.properties.get("versioning") == "true":
                tf_code += "  versioning {\n    enabled = true\n  }\n"
            tf_code += '}\n\n'
    return {"terraform": tf_code}
