from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Depends
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse
from Exploradordir import Searchimg
from pydantic import BaseModel
from platform import platform
from conndb import GesConnMysql
from typing import Dict, List
import asyncio
import uvicorn
import socket
import json
import time
import docker  


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Aquí puedes realizar las tareas de inicio
    print("Iniciando la aplicación...")

    yield

    # Aquí puedes realizar las tareas de cierre
    print("Cerrando la aplicación...")

app = FastAPI(version='1.0.1', lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)

# Middleware para calcular el tiempo de procesamiento
@app.middleware("https")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

class DatosGet(BaseModel):
    servicio: str
    ciudad: int
    tipo: int
    procedimiento: str
    arraydatos: List = []

class DatosUpd(BaseModel):
    servicio: str
    ciudad: int
    procedimiento: str
    arraydatos: List = []

@app.get("/")
def index():    
    return {"Datos": 'En linea!'}

@app.get("/about")
async def about():
    return "Servidor del proyecto bot server Cnd!"

@app.post("/api/v.1/ApiCndCal/GetData")
async def GetSpr(data: DatosGet):    
    try:
        Data = GesConnMysql(data.servicio, data.ciudad).FuncGetSpr(data.tipo, data.procedimiento, data.arraydatos)        
        return {"Datos": Data}
    except Exception as e:        
        return {'Datos': str(e)}


@app.get('/restart_containers')
async def restart_containers(name: str):

    client = docker.from_env()

    # Lista de nombres de contenedores que deseas reiniciar
    containers_to_restart = [name, name.replace("_chrome", "")]  # Cambia estos nombres
    print(containers_to_restart)
    # containers_to_restart = [name]  # Cambia estos nombres

    res = []
    # Reiniciar cada contenedor en la lista
    for container_name in containers_to_restart:
        try:
            # Buscar el contenedor por nombres
            container = client.containers.get(container_name)
            # Reiniciar el contenedor
            container.restart()
            text = f"El contenedor '{container_name}' ha sido reiniciado con éxito."
        except docker.errors.NotFound:
            text = f"No se encontró ningún contenedor con el nombre '{container_name}'."
        except Exception as e:
            text = f"Ocurrió un error al intentar reiniciar el contenedor '{container_name}': {e}"
        
        print(container_name)
        res.append({container_name:text})

    print(res)
    return res


@app.get('/get_dockers')
async def obtener_contenedores():

    client = docker.from_env()
    containers = client.containers.list()
    json_containers = []

    for container in containers:
        if not 'chrome' in container.name:
            continue
        # print(f"Nombre: {container.name}")
        # print(f"ID: {container.id}")
        # print(f"Imagen: {container.image.tags}")
        # print(f"Estado: {container.status}")
        # print(f"Puertos: {container.attrs['NetworkSettings']['Ports']}")
        if not '7900/tcp' in container.attrs['NetworkSettings']['Ports']:
            continue
        Puerto = f"Puertos: {container.attrs['NetworkSettings']['Ports']['7900/tcp'][0]['HostPort']}"
        # print(Puerto)
        # print("-" * 30)
        json_container = {'name': container.name, 'port': Puerto }
        json_containers.append(json_container)

    # print(json_containers)
    return json_containers


@app.get('/Getimagen')
async def obtener_imagen(procedimiento: str, idevento: int, ciudad: str):
    # Conectar a la base de datos y obtener el path de la imagen
    # ciudad = ''
    # ciudad = 'Cali'
    Data = GesConnMysql().FuncGetSpr(procedimiento, ciudad, [idevento])    
    print(Data)

    if 'Windows' in platform():
        if Data:
            Pathimg = Searchimg(Data[0])
            return FileResponse(Pathimg)
        else:
            return FileResponse(r"C:\DBGestionBot\BotcndRazones\Imgnofound.png")

    if Data:    
        normalized_path = Data[0].replace("\\", "/").replace("//", "/")
        relative_path = normalized_path.split("BotcndRazones")[-1]
        path = f"/mnt/images{relative_path}"
        print(path)
        Pathimg = Searchimg(path)
        return FileResponse(Pathimg)
    else:
        return FileResponse("/mnt/images/Imgnofound.png")


async def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 3540))
    ip = s.getsockname()[0]
    config = uvicorn.Config(app, host=ip, port=3541, reload=True)
    server = uvicorn.Server(config)    
    await server.serve()

if __name__ == '__main__':
    asyncio.run(main())
