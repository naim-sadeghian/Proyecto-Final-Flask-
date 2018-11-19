from flask import Flask, request, g, redirect, url_for, render_template, flash, session, json
import ast
app = Flask(__name__)

app.secret_key = "EsteSecreto"


#Inicializacion=======================================
#usuarioOnline= []
with open("vuelosFinal.txt", "r") as arch:
        listaDeVuelos= ast.literal_eval(arch.read())
#=====================================================
@app.route("/", methods=['GET', 'POST'])
def iniciar():
    return render_template("main.html")

@app.route("/ingresar", methods=['GET', 'POST'])
def ingresar():
    global usuarioOnline
    """
    Recibe: el usuario y la password
    Hace: mira a ver que haya un usuario en el archivo de usuario que tenga esa misma clave
            si no encuentra nada, ya sea por que estaba mal el usuario o la clave a los 2
            aparece un flash y lo redirige a la entrada.
    """
    if request.form["boton"] == "entrar":
        arch= open("InfoContactos.txt", "r")
        if arch.readline() == "":
            listaTemp= []
            
        else:
            with open("InfoContactos.txt", "r") as arch:
                listaTemp= ast.literal_eval(arch.read()) #El ast. es una biblioteca que me permite transformar archivos a listas
        arch.close

        
        #revisa que exista el usuario==========================================================================================
        i= 0
        while i < len(listaTemp): 
            if (listaTemp[i]["usuario"] == request.form["usuario"]) and(listaTemp[i]["usuario"] == request.form["usuario"]):
                usuarioOnline= listaTemp[i]
                return render_template("buscador.html", usuarioOnline=usuarioOnline)
                
            i= i+1
        #======================================================================================================================
        #Si no lo encuentra====================================================================================================
        if i == len(listaTemp):
            flash("No se encontraron coincidencias")
            return redirect(url_for("iniciar"))
    
@app.route("/crear", methods=['GET', 'POST'])
def crear():
    return render_template("crear.html")

@app.route("/registrar", methods=['GET', 'POST'])
def registrar():
    """
    Recibe: nombre, usuario, password, preferencias
    Hace: primero revisa que el usuario digitado no sea uno en uso, si esta en uso muestra un flash y lo regresa a la entrada.
            Luego escribe la informacion del usuario nuevo en un archivo de texto= InfoContactos.txt
    """

    global usuarioOnline

    if request.method == "POST":
        if request.form["boton"]== "Crear Cuenta":      

            arch= open("InfoContactos.txt", "r")
            if arch.readline() == "":
                listaTemp= []
                
            else:
                with open("InfoContactos.txt", "r") as arch:
                    listaTemp= ast.literal_eval(arch.read())
            arch.close
            #revisa que no exista el usuario=======================================================
            i= 0
            while i < len(listaTemp): 
                if listaTemp[i]["usuario"] == request.form["usuario"]:
                    flash("Este usuario ya existe. Vuelva a probar con uno nuevo")
                    return redirect(url_for('crear'))
                i= i+1
                
            if i == len(listaTemp):
            
                nombre= request.form["nombre"]
                apellido= request.form["apellido"]
                usuario= request.form["usuario"]
                password= request.form["password"]
                preferencias=[]
                preferencias= request.form.getlist("preferencias") #recibe las checkboxes marcadas como lista
                
                infoTemp={"nombre": nombre, "apellido": apellido, "usuario": usuario,
                                    "password": password, "preferencia": preferencias, "historial": []}
                listaTemp.append(infoTemp)

                usuarioOnline= infoTemp
                

                with open("InfoContactos.txt", "w") as arch:
                    arch.write(str(listaTemp))
                
                return redirect(url_for('iniciar'))
	
            #========================================================================================
@app.route("/Buscar", methods=['GET', 'POST'])
def buscarVuelo():
    """
    Busqueda Normal:
        Recibe: la ciudad de salida y de origen
        Hace: revisa que no sea la misma ciudad, si lo es, aparece un flash y lo regresa.
                Imprime una lista con todos los vuelos directos al destino.
                En caso de que no encuentre vuelos directos. Crea otra lista con todas las conexiones posibles de maximo una parada.
                
    Busqueda Con Preferencia:
        Busca vuelos directos como la busqueda normal, pero tambien revisa que sea en aerolineas que pertenecen a
        la lista de sus preferidas.

    Editar Preferencias:
        Lo lleva a la pagina para editar preferencias
        
    Salir:
        Saca al usuario de regreso a la pantalla de entrada
    """
    global usuarioOnline, listaDeVuelos
    posiblesVuelos= []
    lengthTemp= 0
    
    if request.method == "POST":
        #BUSCAR NORMAL==============================================================================
        #===========================================================================================
        if request.form["boton"] == "Buscar Vuelo":
            cOrigen = request.form.get("sel_origen")
            cDestino = request.form.get("sel_destino")

            if cOrigen == cDestino: #Si la ciudad de llegada y la de salida son iguales=============
                flash("La ciudad de origen y destino son iguales. Porfavor intentar de nuevo.")
                return render_template("buscador.html", usuarioOnline=usuarioOnline)
            else:
                
                i = 0
                while i < len(listaDeVuelos):
                    if (listaDeVuelos[i][0]['origen'] == cOrigen) and (listaDeVuelos[i][0]['destino'] == cDestino):
                        posiblesVuelos.append(listaDeVuelos[i])
                        
                    i= i+1
                lengthTemp= len(posiblesVuelos)
                print("el len es: ", len(posiblesVuelos))
                
                if len(posiblesVuelos) == 0:
                    flash("No hay vuelos directos, pero aqui hay una lista de conexiones")
                    #BUSCAR CONEXION
                    #=================================================================================================
                    
                    posiblesSalidas= []
                    posiblesLlegadas= []
                    midCity= ["ABQ","ATL", "BNA", "BOS", "DCA", "DEN", "DFW", "DTW", "HOU", "JFK", "LAX", "TPA",
                              "MIA", "MSP", "MSY","ORD", "PHL", "PHX", "PVD", "RDU", "SEA", "SFO", "STL" ]
                    conexion1 = []
                    conexion2 = []
                    
                    for city in midCity:
                        z= 0
                        while z < len(listaDeVuelos):
                            if (listaDeVuelos[z][0]['origen'] == cOrigen) and (listaDeVuelos[z][0]['destino'] == city):
                                posiblesSalidas.append(listaDeVuelos[z])
                            z += 1
                            
                    for city in midCity:
                        w= 0
                        while w < len(listaDeVuelos):
                            if (listaDeVuelos[w][0]['origen'] == city) and (listaDeVuelos[w][0]['destino'] == cDestino):
                                posiblesLlegadas.append(listaDeVuelos[w])
                            w += 1
                            
                    
                    for salida in posiblesSalidas:
                        count= 0
                        while count < len(posiblesLlegadas):
                            if salida[0]["destino"] == posiblesLlegadas[count][0]["origen"]:
                                conexion1.append(salida)
                                conexion2.append(posiblesLlegadas[count])
                            count +=1                        
                   
                    lengthTemp= len(conexion1)

                    
                    return render_template("conexion.html", usuarioOnline=usuarioOnline, conexion1=conexion1, conexion2=conexion2, lengthTemp=lengthTemp)
                    #=================================================================================================
                else:
                    return render_template('reservar.html', posiblesVuelos=posiblesVuelos, lengthTemp=lengthTemp)
               
        #===========================================================================================
        #BUSCAR CON PREFERENCIAS
        if request.form["boton"] == "Buscar Con Preferencias":
            cOrigen = request.form.get("sel_origen")
            cDestino = request.form.get("sel_destino")
            
            if cOrigen == cDestino: #Si la ciudad de llegada y la de salida son iguales=============
                flash("La ciudad de origen y destino son iguales. Porfavor intentar de nuevo.")
                return render_template("buscador.html", usuarioOnline=usuarioOnline)
            else:
                pref= usuarioOnline["preferencia"]
                i = 0
                while i < len(listaDeVuelos):
                    if (listaDeVuelos[i][0]['origen'] == cOrigen) and (listaDeVuelos[i][0]['destino'] == cDestino):
                        posiblesVuelos.append(listaDeVuelos[i])
                    i= i+1
                lengthTemp= len(posiblesVuelos)
                #Revisa que se cumplan las preferencias
                y = 0
                nuevosVuelos= []
               
                for li in posiblesVuelos:
                    if li[0]["aerolinea"] in usuarioOnline["preferencia"]:
                        nuevosVuelos.append(li)
                        lengthTemp= lengthTemp - 1
                    y += 1
                #=====================================
                print(nuevosVuelos)
                print(len(nuevosVuelos))
                if len(nuevosVuelos) == 0:
                    flash("No hubo vuelos encontrados con sus preferencias")
                    return render_template("buscador.html", usuarioOnline=usuarioOnline)
                else:
                    return render_template('reservar.html', posiblesVuelos=nuevosVuelos, lengthTemp=lengthTemp)
        #======================================================================================================
        #EDITAR PREFERENCIAS
        if request.form["boton"] == "Editar Preferencias":
            return render_template("editar.html", usuarioOnline=usuarioOnline)
        #======================================================================================================
        #CERRAR SESSION
        if request.form["boton"] == "Salir":
            return redirect(url_for("iniciar"))
   
@app.route("/Reservar", methods=['GET', 'POST'])
def reservarVuelo():
    """
    Recibe: el numero del vuelo escogido en el radio del html
    Hace: inserta el vuelo en la etiqueta de historial para el usuario en el archivo de texto = InfoContactos.txt
    """
    global usuarioOnline
    if request.method == "POST":
        if request.form["boton"]== "Reservar Vuelo":
            option = request.form["radio"]
            
            usuarioOnline["historial"].append(option)
            aux= []
            #Lo escribe en el archivo============================
            with open("InfoContactos.txt", "r") as arch:
                aux= ast.literal_eval(arch.read())
            cont= 0

            while cont < len(aux):
                if aux[cont]["usuario"] == usuarioOnline["usuario"]:
                    aux[cont]["historial"].append(option)
                    with open("InfoContactos.txt", "w") as arch:
                        arch.write(str(aux))
                        
                cont= cont + 1
                    
            #====================================================
                
            return render_template("buscador.html", usuarioOnline=usuarioOnline)

@app.route("/ReservarConexion", methods=['GET', 'POST'])
def reservarConexion():
    """
    Recibe: los dos numeros de vuelo para la conexion de vuelos
    Hace: instera los numeros de vuelo en la etiqueta 'historial' del usuario en el archivo de texto = InfoContactos.txt
    """
    global usuarioOnline
    if request.method == "POST":
        if request.form["boton"]== "Reservar Vuelo":
            option = "cnx" + str(request.form["radio"])

            usuarioOnline["historial"].append(option)
            aux= []
            #Lo escribe en el archivo============================
            with open("InfoContactos.txt", "r") as arch:
                aux= ast.literal_eval(arch.read())
            cont= 0

            while cont < len(aux):
                if aux[cont]["usuario"] == usuarioOnline["usuario"]:
                    aux[cont]["historial"].append(option)
                    with open("InfoContactos.txt", "w") as arch:
                        arch.write(str(aux))
                        
                cont= cont + 1
            
                    
            #====================================================
                
            return render_template("buscador.html", usuarioOnline=usuarioOnline)

@app.route("/EditarPreferencia", methods=['GET', 'POST'])
def editarPref():
    """
    Recibe: una lista con la nueva configuracion de preferencias
    Hace: remplaza las preferencias del usuario pasadas en el archivo de texto = InfoContactos.txt
    """
    global usuarioOnline
    
    if request.method == "POST":
        if request.form["boton"]== "Editar":
            with open("InfoContactos.txt", "r") as arch:
                listaTemp= ast.literal_eval(arch.read())
                
            nuevoPref= request.form.getlist("preferencias")
            usuarioOnline["preferencia"]= nuevoPref
            i= 0
            while i < len(listaTemp):
                if listaTemp[i]["usuario"] == usuarioOnline["usuario"]:
                    listaTemp[i]["preferencia"] = nuevoPref
                    print("Encontro alguien pa cambiar")
                i += 1
            
            with open("InfoContactos.txt", "w") as arch:
                arch.write(str(listaTemp))
            
            return render_template("buscador.html", usuarioOnline=usuarioOnline)

if __name__== "__main__":
    app.run(debug=True)
