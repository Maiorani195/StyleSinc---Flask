
import csv
from flask import Blueprint, jsonify,request,current_app
from app.models.user import LoginPayload
from pydantic import ValidationError
from app import db
from bson import ObjectId
from app.models.sale import Sale
from app.models.products import ProductDBModel
from app.decorators import token_required
from datetime import datetime, timedelta, timezone
import jwt
import os 
import io
main_bp = Blueprint('main', __name__)




# RF: o sistema deve permitir que o usuario que um usuario se autenique para pegar um token
@main_bp.route('/login' , methods=['POST'])
def login():
    try:
      raw_data=request.get_json()
      user_data = LoginPayload(**raw_data)
     
    except ValidationError as e:
        return jsonify({"error": "Dados de login inválidos", "details": e.errors()}), 400
    except Exception as e:
        return jsonify({"erro:" : "Corpo da requisiçao invalido , nao é um json!"}), 400
   
    if user_data.username  == 'admin' and user_data.password == '1234':
       token = jwt.encode(
            {
            "user_id": user_data.username,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )       
       return jsonify({"token": token}), 200
   
    return jsonify({"error": "Credenciais inválidas!"}), 401









# RF: O sistema deve permitir a listagem de todos os produtos







@main_bp.route('/products', methods=['GET'])
def get_products():
    products_cursor = db.products.find()
    products_list = [ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True) for product in products_cursor]
    return jsonify(products_list), 200 





# RF: O sistema deve permitir a entrada de um novo produto 

@main_bp.route('/products', methods=['POST'])
@token_required
def create_product(token):
    try:
        new_product = ProductDBModel(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": "Dados de produto inválidos", "details": e.errors()}), 400
    except Exception as e:
        return jsonify({"erro:" : str(e)}), 500
    
    result = db.products.insert_one(new_product.model_dump(by_alias=True, exclude_none=True))

    return jsonify({"mensagem": "Bem vindo à rota de criação de produto",
                    "id": str(result.inserted_id)}) , 201





# RF: O sistema deve permitir a atualização de um produto








@main_bp.route('/products/<string:product_id>', methods=['PUT'])
@token_required
def update_product(token,product_id):
  
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify({'error': 'ID de produto em formato inválido'}), 400


    try:
        update_data = ProductDBModel(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": "Dados de produto inválidos", "details": e.errors()}), 400
    
  
    update_result = db.products.update_one({'_id': oid}, {'$set': update_data.model_dump(by_alias=True, exclude_unset=True)})
    
    if update_result.matched_count == 0:
        return jsonify({"error": f"Produto com id {product_id} não encontrado!"}), 404
        
    updated_product = db.products.find_one({'_id': oid})
    product_model = ProductDBModel(**updated_product).model_dump(by_alias=True, exclude_none=True)
    
    return jsonify(product_model)



# RF: O sistema deve permitir a exclusão de um produto




# RF: O sistema deve permitir a exclusão de um produto
@main_bp.route('/products/<string:product_id>', methods=['DELETE'])
@token_required
def delete_product(token, product_id):

    try:
        oid = ObjectId(product_id)
    except Exception as e:
       
        return jsonify({'error': 'ID de produto em formato inválido'}), 400

    
    delete_result = db.products.delete_one({'_id': oid})
    
    
    if delete_result.deleted_count == 0:
       
        return jsonify({'error': f'Produto com id {product_id} não encontrado!'}), 404
        
    
    
    return "", 204

#RF: O sistema deve permitir a visualização de um produto específico
@main_bp.route('/products/<string:product_id>', methods = ['GET'])
def get_product(product_id): 
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar o produto {product_id}: {e}'}), 500
    product = db.products.find_one({'_id': oid})
    if product:
        product_model = ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
        return jsonify(product_model)
    else:
        return jsonify({'error': f'Produto com o id {product_id} não encontrado'}),404
   
#RF: o sistema deve permitir  a importaçao de vendas atraves de um arquivo csv
@main_bp.route('/importar-vendas', methods=['POST'])
def import_vendas():
    return jsonify({"mensagem": "Bem vindo à rota de importação de vendas!"})


@main_bp.route('/')
def index():
    return jsonify({"mensagem": "Bem vindo à  StyleSinc!"})



@main_bp.route('/sales/upload', methods=['POST'])
@token_required
def upload_sales(token):
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado!"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado!"}), 400
    
    if file and file.filename.endswith('.csv'):
        # Correção 1: Removido o "as csvfile:" e os dois pontos finais
        csv_stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(csv_stream)
        
        sales_to_insert = []
        error = []

        for row in enumerate(csv_reader, 1):
            # Correção 2: Alinhamento perfeito do bloco try/except
            try:
                sale_data = Sale(**row[1])
                # Correção 3: Trocado ponto por underline (sales_to_insert)
                sales_to_insert.append(sale_data.model_dump())
            except ValidationError as e:
                error.append(f'Linha {row[0]}: Dados de venda inválidos')
            except Exception as e:
                error.append(f'Linha {row[0]} com erro inesperado: {str(e)}')
          
        if sales_to_insert:
            try:
                db.sales.insert_many(sales_to_insert)
            except Exception as e:
                # Correção 4: Convertendo 'e' para string
                return jsonify({"error": str(e)}), 500
                
        return jsonify({
            "message": "Upload de vendas realizado com sucesso!",
            "vendas_importadas": len(sales_to_insert),
            "erros_encontrados": error
        }), 200

   
   