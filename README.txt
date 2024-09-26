This is prepped to run in a VPC Linux Ubuntu server.

To run the API and make it be available 24/7 carry out the next steps:

1 Install docker if it is not installed in your server
2 docker build -t kavak_webhook .
3 docker run -d -p 5000:5000 kavak_webhook


Asistente virtual para Kavak 

Enlace de whatsapp para comunicarse con el BOT: https://wa.link/wg7wfz -> importante: antes de usar enviar el siguiente mensaje para activarlo: join back-greatly 


Roadmap para llevarlo a producción: 

La primera opción que consideraría para llevarlo a producción es pasar lo que es el servidor de Flask a una función Lambda en AWS. 

La segunda opción, es utilizar elastic beanstalk para deployar el servidor de Flask. 

La tercera (la que está ahora en funcionamiento) es utilizar Docker. En caso de que este en producción sería conveniente que venga con un Volumen para poder mantener la consistencia de data del contenedor en caso de que se detenga. 

La cuarta es utilizar un clúster de Kubernetes (no tengo experiencia práctica, pero si conocimiento teórico del uso de kubernetes para mantener la aplicación en funcionamiento y generar algo similar a lo que sería un balanceador de carga). 

 			 		Como evaluaría el desempeño del bot: 

Guardaria en un json / base de datos donde se evaluaría cuanto se tarda cada respuesta del chatbot. Tambien se podría hacer un openai functions para cada vez que el bot envía el link a la página de kavak para que la persona efectúe una compra. También seria útil poder guardar la cantidad de respuestas que envía por dia y hasta por hora. 

		¿Cómo probarías que una nueva versión del agente no tiene retroceso en su funcionalidad? 

Se podrían utilizar pruebas unitarias en el CICD para asi verificar si el bot sigue contestando como debería. Se podria utilizar librería como Pytest. 

Me parecería muy importante tener 2 bots corriendo, uno para testeos y otro en producción. 

Teniendo así la rama dev y prod. La rama dev seria una extensión de prod donde se haría testeos de las nuevas modificaciones. Todas las modificaciones del bot deberían hacerse en dev. Una vez testeadas, se haría un pull request de dev hacia prod. Una vez aceptado este pull requests, se correría un CICD de github actions para que se hagan los cambios y el deploy de la nueva versión que se paso a prod. 

 

 

⁠Manual para que cualquier persona pueda instalar el bot. 

    A lo largo de esta guia, se irán detallando las variables necesarias en nuestro archivo .env el cual no estará en el repositorio por obvias razones de seguridad. El archivo .env necesitara de las siguientes KEYS:  


    Crear una cuenta de Twilio y setear un numero de prueba. En el siguiente link se detalla muy concisamente como hacerlo: https://www.youtube.com/watch?v=UVez2UyjpFk 

    De este paso obtendremos la variable TWILIO_NUMBER = "+123456789" (importante el numero) 

    Tambien deberemos setear la variable ACCOUNT_SID y AUTH_TOKEN con estos valores 

    En sandbox settings, setear el ip de nuestro vpc + puerto para que Twilio haga una petición de tipo POST a nuestro endpoint para así procesar el mensaje de texto que enviemos por WhatsApp al número de prueba. 

    Ingresar a nuestro vpc via SSH. 

    Moverse a la carpeta home, crear una carpeta con el nombre del proyecto 

    Hacer un git clone del repositorio del proyecto https://github.com/GastonGaitan/Kavak-Chatbot/tree/master 

    Luego, como en todo proyecto de python, crear el entorno virtual e instalar las dependencias del requirements.txt 

    Antes de seguir, vamos a necesitar una apikey de Openai. Esta tendrá que estar en nuestro archivo .env como OPENAI_API_KEY. 

    Ejecutar el archivo create_assitant.py 

    La ejecucion del script hara que se cree un Openai Assistant y se printee en pantalla de la terminal el assistant id. Esto se usará para llenar la variable de entorno .env KAVAK_ASSISTANT_ID. 
    
    Ahora a dockerizar la aplicación para que corra sin dificultades en el background. 

    Creamos la imagen.

    Corremos el contenedor en modo –d para que quede corriendo en el background. 

    Resta enviarle un mensaje a nuestro chatbot de twilio para que este redirija el mensaje hacia nuestro servidor de Flask. 

    Se recibe el mensaje en el servidor de flask, se envia al asistente de openai y se retorna la respuesta usando el sdk de twilio. 

    Felicitaciones, ya tenes tu chatbot de Kavak Funcionando.  
    

 

Diagrama de prompts. 

    El prompt mas importante son las isntrucciones que se le agregan al asistente en el siguiente segmento de codigo en el archivo create_assistant.py:

    # Assistant creation
    kavak_ai_assistant = client.beta.assistants.create(
        assistant_id=os.environ["KAVAK_ASSISTANT_ID"], 
        name="Asistente de IA de Kavak",
        instructions=f'''
        Asistente de IA de Kavak para ayudar con atención al cliente.
        Vas al grano, no te extiendas demasiado en tus respuestas.
        Tus respuestas no pueden exceder los 1500 caracteres. Siempre trata de ser lo mas breve posible.
        Esta es informacion de la empresa y el modelo de negocio de Kavak: {kavak_business_data}
        No puedes involucrarte en ninguna convesarción que no tenga que ver con autos y el negocio de Kavak.
        Dependiendo del auto por el que la persona se sienta interesada, seras capaz de otorgar 
        planes de financiamiento tomando como base el enganche, el precio
        del auto, una tasa de interés del 10% y plazos de financiamiento de entre 3 y 6 años.
        Informacion de nuestros vehiculos disponibles de los cuales deberas proporcionar informacion y buscar cerrar ventas: ꐕ{kavak_cars_data}ꐕ
        Importante, solamente brindaras informacion de los autos que se encuentran en el json delimitado entre los simbolos ꐕ.
        ''',
        model="gpt-4o",
    )


    Por ensayo y error, en mi experiencia he encontrado muy útil utilizar símbolos muy poco comunes como "ꐕ" para que la IA pueda tener una facilidad más grande a la hora de delimitar que contenido es con el que debe contestar únicamente. Yo creo que la IA de Openai tiene funcionalidades similares en ciertos momentos a lo que son las Regular Expressions. Teniendo eso en cuenta, considero que es una buena práctica delimitar cierto contenido con símbolos poco comunes para aclarar que ciertas respuestas solo deben basarse en ese contenido rodeado por los símbolos poco comunes. 

    Otra forma también es utilizar Vector Storage para agregarle conocimiento. 

    No obstante, en mi experiencia, utilizar este tipo de delimitaciones ha sido muy acetada. 

    La desventaja es que se puede llegar a superar el límite de tokens. 

    Creo que es la solución más rápida para poner en práctica el Bot, pero no la más eficiente en términos de escalabilidad. 

    Además, la instrucción busca definir que la respuesta no se exceda de los 1500 caracteres para así evitar superar el límite de 1600 que tiene Twilio. 

    Se le hace énfasis en que su objetivo es cerrar ventas. 

    Otros enfoques que se podrían hacer para obtener kavak_cars_data: 

    Hacer una Openai función que obtenga data de una api o base de datos de Kavak con los autos disponibles en la página. 

    Agregar conocimiento de todos los autos que tenga Kavak a una vector storage y alinearla al asistente de Openai para que así pueda dar recomendaciones más detalladas como si fuera un mecánico / experto en autos. 