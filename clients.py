import pymysql
from app import app
from bd_clients import mysql
from flask import jsonify
from flask import flash, request,Response
from auth import BasicAuth

	
@app.route("/api/clientes", methods=["POST"])  #Inclui um registro no banco
def add_clients():
	try:

		_json=request.json
		_Nome=_json['Nome']
		_CPF=_json['CPF']
		_Email=_json['Email']
		_Telefone=_json['Telefone']

		conn=mysql.connect()
		cursor=conn.cursor()
		
		
		if _Nome and _CPF and _Email and _Telefone and request.method=="POST":
			
			sqlQuery="INSERT INTO CLIENTES (Nome, CPF, Email, Telefone) VALUES (%s,%s, %s, %s);"
			bindData=(_Nome, _CPF, _Email, _Telefone)
			cursor.execute(sqlQuery,bindData)
			conn.commit()
			response = jsonify('Cadastrado com sucesso!')
			response.status_code=200
			return response

		else:
			return  jsonify({"error":f"Erro"}),500
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
			cursor.close() 
			conn.close()

			
			

@app.route('/api/clientes/<int:id_cliente>', methods=['PUT'])
def update_clients(id_cliente):
	try:
		conn = mysql.connect()
		cursor=conn.cursor()
		
		sqlQuery = "SELECT * FROM clientes WHERE id_cliente=%s"
		cursor.execute(sqlQuery,id_cliente)
		select = cursor.fetchone()
		if not select:
			return Response('Cliente não cadastrado', status=400)
		
		_json = request.json
		
		_Nome = _json['Nome']
		_CPF = _json['CPF']
		_Email = _json['Email']
		_Telefone = _json['Telefone']
		_id_cliente = _json['id_cliente']
		

		if _Nome and _CPF and _Email and _Telefone and _id_cliente and request.method == 'PUT':
			
			sqlQuery = "UPDATE clientes SET Nome=%s, CPF=%s, Email=%s, Telefone=%s WHERE id_cliente=%s"
			bindData = (_Nome, _CPF, _Email, _Telefone, _id_cliente,)
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			response = jsonify('Alterado atualizado com sucesso!')
			response.status_code = 200
			return response
		else:
			return  jsonify({"error":f"Erro"}),500
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
			cursor.close() 
			conn.close()
  
@app.route('/api/clientes/<int:id_cliente>', methods=['DELETE']) #Apaga um registro do banco
def delete_clients(id_cliente):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		sqlQuery = "SELECT * FROM clientes WHERE id_cliente=%s"
		cursor.execute(sqlQuery, id_cliente)
		select = cursor.fetchone()
		if not select:
			return jsonify('Cliente não cadastrado.') , 404
		cursor.execute("DELETE FROM clientes WHERE id_cliente =%s", (id_cliente))
		conn.commit()
		response = jsonify('Cliente deletado com sucesso!')
		response.status_code = 200
		return response
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close() 
		conn.close()


@app.route('/api/clientes')  #Consulta todas os registros do banco
def show():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM clientes;")
		showRows = cursor.fetchall()
		response = jsonify(showRows)
		response.status_code = 200
		return response
	except Exception as error:
		return jsonify({"error":f"{error}"}),500
	finally:
		cursor.close() 
		conn.close()


@app.route('/api/clientes/<int:id_cliente>', methods=["GET"]) #Consulta um registro no banco
def view_clients(id_cliente):

	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT id_cliente, nome, cpf, email, telefone FROM clientes WHERE id_cliente =%s", id_cliente)
		view_Rows = cursor.fetchall()
		if not view_Rows:
				return Response("Usuário não encontrado."), 404
		response = jsonify(view_Rows)
		response.status_code = 200
		return response     
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close() 
		conn.close()

@app.route('/api/clientes/<int:id_cliente>/enderecos', methods=["GET"])  #Consulta todas os registros de endereço do cliente através do seu id 
def show_client_endereco(id_cliente):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT enderecos.CEP,enderecos.Endereco,enderecos.Numero,enderecos.Complemento,enderecos.Bairro,enderecos.Localidade,enderecos.UF FROM cadastro1.enderecos inner  join  cadastro1.clientes on clientes.id_cliente = enderecos.id_cliente   WHERE enderecos.id_cliente = %s ",id_cliente )
        showRows = cursor.fetchall()
        if not showRows:
            return Response("Não encontrado."),404
        response = jsonify(showRows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

if __name__ == "__main__":
   app.run(debug=True)
   