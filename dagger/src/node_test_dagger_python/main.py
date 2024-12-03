import random

import dagger 
from dagger import dag, function, object_type


@object_type
class NodeTestDaggerPython:
    @function
    async def publish(self, source: dagger.Directory) -> str:
        """Publish the application container after building and testing it on-the-fly"""
        await self.test(source)
        await self.build_env(source).with_exec(["npm", "install"]).stdout()
        await self.build_env(source).with_exec(["npm", "run", "test"]).stdout()

        return "publicacion completada"
    

    @function
    async def test_pipeline(self, source: dagger.Directory) -> str:
        """Prueba el pipeline de GitHub Actions"""

        
        pipeline_yaml_path = "/.github/workflows/node.js.scan.yml"
        
        #async with dagger.connect() as client:
        client = await dagger.connect()  # Correcto: conectamos asincrónicamente
        
        # Crear el contenedor desde la imagen base de Ubuntu
        container = await client.container("ubuntu:latest") #container = await dagger.Container.from("ubuntu:latest")

        
        print("Realizando checkout del repositorio...")

        # Aquí podrías agregar más pasos si es necesario, como hacer run del pipeline o pruebas adicionales.

        # Retornar un mensaje de éxito
        return "ok comunicación"
        

    @function
    async def build(self, source: dagger.Directory) -> str:
        """Construir el proyecto (si es necesario)"""
        # Instalar dependencias
        await self.build_env(source).with_exec(["npm", "install"]).stdout() 

        # Ejecutar pruebas
        await self.build_env(source).with_exec(["npm", "run", "test"]).stdout()

        # Aquí omitimos el paso de "npm run build"
        # await self.build_env(source).with_exec(["npm", "run", "build"]).stdout()

        return "Construcción completada"
        
        #return (
         #   dag.container()
          #  .from_("nginx:1.25-alpine")
           # .with_directory("/usr/share/nginx/html", build)
            #.with_exposed_port(80)
        #)

    @function
    async def test(self, source: dagger.Directory) -> str:
        """Return the result of running unit tests"""
        #return await (
         #   self.build_env(source)
          #  .with_exec(["npm", "run", "test"])  # Usamos el script 'test' que ya está definido en package.json
           # .stdout()

           
        #)
    
        return "ok test"


    @function
    def build_env(self, source: dagger.Directory) -> dagger.Container:
        """Build a ready-to-use development environment"""
        node_cache = dag.cache_volume("node")
        
        return (
            dag.container()
            .from_("node:21-slim")
            .with_directory("/src", source)
            .with_mounted_cache("/root/.npm", node_cache)
            .with_workdir("/src")
            .with_exec(["npm", "install"])

            
        )