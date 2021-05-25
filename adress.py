import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request,Response
from auth import BasicAuth



@app.route("/api/enderecos", methods=["POST"])  #Inclui um registro no banco
def add_adress():
	try:

		_json=request.json
		_id_cliente=_json['id_cliente']
		_CEP=_json['CEP']
		_Endereco=_json['Endereco']
		_Numero=_json['Numero']
		_Complemento=_json['Complemento']
		_Bairro=_json['Bairro']
		_Localidade=_json['Localidade']
		_UF=_json['UF']



		conn=mysql.connect()
		cursor=conn.cursor()
		
		
		if _id_cliente and _CEP and _Endereco and _Numero and _Complemento and _Bairro and _Localidade and _UF and request.method=="POST":
			
			sqlQuery="INSERT INTO enderecos (id_cliente,CEP,Endereco,Numero,Complemento,Bairro,Localidade,UF) VALUES (%s,%s,%s,%s,%s, %s, %s, %s);"
			bindData=(_id_cliente,_CEP, _Endereco,_Numero, _Complemento, _Bairro,_Localidade,_UF)
			cursor.execute(sqlQuery,bindData)
			conn.commit()
			response = jsonify('Cadastrado com sucesso!')
			response.status_code=200
			return response

		else:
			return  jsonify({"error":f"Erro"}),500	
	except Exception as error:
		return jsonify({"error":f"{error}"}),500
	finally:
			cursor.close() 
			conn.close()

@app.route("/api/enderecos/<int:id_end>", methods=["PUT"])  #Inclui um registro no banco
def update_adress(id_end):
	try:
		conn = mysql.connect()
		cursor=conn.cursor()
		
		sqlQuery = "SELECT * FROM enderecos WHERE id_end=%s"
		cursor.execute(sqlQuery,id_end)
		select = cursor.fetchone()
		if not select:
			return Response('Endereço não cadastrado', status=400)

		_json=request.json
		_id_cliente =_json['id_cliente']
		_id_end=_json['id_end']
		_CEP=_json['CEP']
		_Endereco=_json['Endereco']
		_Numero=_json['Numero']
		_Complemento=_json['Complemento']
		_Bairro=_json['Bairro']
		_Localidade=_json['Localidade']
		_UF=_json['UF']


		
		
		if _id_cliente and _CEP and _Endereco and _Numero and _Complemento and _Bairro and _Localidade and _UF and _id_end and request.method =="PUT":
			sqlQuery="UPDATE enderecos SET id_cliente=%s ,CEP=%s ,Endereco=%s,Numero=%s ,Complemento= %s ,Bairro= %s ,Localidade= %s ,UF= %s  WHERE id_end = %s"
			bindData=(_id_cliente,_CEP, _Endereco,_Numero, _Complemento, _Bairro,_Localidade,_UF,_id_end,)
			cursor.execute(sqlQuery,bindData)
			conn.commit()
			response = jsonify('Alterado com sucesso com sucesso!')
			response.status_code=200
			return response

		else:
			return  jsonify({"error":f"Erro"}),500
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
			cursor.close() 
			conn.close()            
			



@app.route('/api/enderecos/<int:id_end>', methods=['DELETE']) #Apaga um registro do banco
def delete_adress(id_end):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		sqlQuery = "SELECT * FROM enderecos WHERE id_end=%s"
		cursor.execute(sqlQuery, id_end)
		select = cursor.fetchone()
		if not select:
			return jsonify('Endereço não cadastrado.') , 400
		cursor.execute("DELETE FROM enderecos WHERE id_end =%s", (id_end))
		conn.commit()
		response = jsonify('Deletado com sucesso!')
		response.status_code = 200
		return response
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close() 
		conn.close()


@app.route('/api/enderecos')  #Consulta todas os registros do banco

def show_address():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM enderecos")
		showRows = cursor.fetchall()
		response = jsonify(showRows)
		response.status_code = 200
		return response
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close() 
		conn.close()

	  



@app.route('/api/enderecos/<int:id_end>', methods=["GET"]) #Consulta um registro no banco  através do Id_end
def view_adress(id_end):
   
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT  id_cliente,id_end,CEP,Endereco,Numero,Complemento,Bairro,Localidade,UF FROM enderecos WHERE id_end = %s",  id_end )
		view_Rows = cursor.fetchall()
		if not view_Rows:
			return Response("Endereço não encontrado"),404
		response = jsonify({'result':view_Rows,'status':200,})	
		return response		

	except Exception as error:
		return jsonify({"error":f"{error}"}), 500

	finally:
		cursor.close() 
		conn.close()

@app.route('/clientes/<int:id_cliente>/enderecos', methods=["GET"])  #Consulta todas os registros de endereço do cliente através do seu id 
def clients_end(id_cliente):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT enderecos.CEP,enderecos.Endereco,enderecos.Numero,enderecos.Complemento,enderecos.Bairro,enderecos.Localidade,enderecos.UF,enderecos.id_cliente,clientes.Nome FROM enderecos inner  join  clientes on clientes.id_cliente = enderecos.id_cliente   WHERE enderecos.id_cliente = %s ",id_cliente )
		showRows = cursor.fetchall()
		if not showRows:
			return Response("Cliente não encontrado.")
		response = jsonify(showRows)
		response.status_code = 200
		return response
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close() 
		conn.close()               

if __name__ == "__main__":
	app.run(debug=True,port =5003)
