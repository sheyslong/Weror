from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    keys= '/keys/'
    companies= '/companies/'
    numberDocument = '/numberDocument/'

    from app.models import Chaves, Company, NumberDocument

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route(keys, methods=['GET'])
    def getKeys():
        chaves = Chaves.query.filter_by(status='Free').limit(64)
        res = {}
        for chave in chaves:
            chave.status = 'Using'
            db.session.commit()

            res[chave.id] = {
                'id': chave.id,
                'status': chave.status
            }          
                
        return jsonify(res)

    @app.route('/set/', methods=['GET'])
    def setStatus():
        chaves = Chaves.query.filter_by(status='Using')
        res = {}
        for chave in chaves:
            chave.status = 'Free'
            db.session.commit()

            res[chave.id] = {
                'id': chave.id,
                'status': chave.status
            }          
                
        return jsonify(res)

    @app.route('/using/', methods=['GET'])
    def getStatusUsing():
        chaves = Chaves.query.filter_by(status='Using')
        res = {}
        for chave in chaves:
            res[chave.id] = {
                'id': chave.id,
                'status': chave.status
            }          
                
        return jsonify(res)

    @app.route('/free/', methods=['GET'])
    def getStatusFree():
        chaves = Chaves.query.filter_by(status='Free')
        res = {}
        for chave in chaves:
            res[chave.id] = {
                'id': chave.id,
                'status': chave.status
            }          
                
        return jsonify(res)

    @app.route('/ok/', methods=['GET'])
    def getStatusOK():
        chaves = Chaves.query.filter_by(status='Ok')
        res = {}
        for chave in chaves:
            res[chave.id] = {
                'id': chave.id,
                'status': chave.status
            }          
                
        return jsonify(res)


    @app.route(keys+'<id>', methods=['GET'])
    def getKeyId(id):
        if isNull(id):
            return jsonify({'return':'Id is Null!'})

        chave = Chaves.query.filter_by(id=str(id)).first()
        if not chave:
            return jsonify({'return':'Key not exist!'})
        res = {
            'id': chave.id,
            'status': chave.status
        }

        return jsonify(res)

    @app.route(keys, methods=['POST'])
    def postKey():
        id = request.form.get('id')

        if isNull(id):
            return jsonify({'return':'ID null!'})
        else:
        	chave = Chaves(str(id))
        	db.session.add(chave)
        	db.session.commit()
        	return jsonify({'id': chave.id})

    @app.route(keys, methods=['PUT'])
    def putKey():
        id = request.form.get('id')
        status = request.form.get('status')

        if isNull(id) or isNull(status):
            return jsonify({'return':'Values Null!'})

        chave = Chaves.query.filter_by(id=id).first()
        
        if not chave:
            return jsonify({'return': 'Not Exist'})
        else:
            chave.status = str(status)
            db.session.commit()
            chave = Chaves.query.filter_by(id=id).first()
            return jsonify({'id': chave.id, 'status': chave.status})
    
    @app.route(keys, methods=['DELETE'])
    def deleteKey():
        id = request.form.get('id')

        if isNull(id): 
            return deleteKeys()
        else:
            chave = Chaves.query.filter_by(id=id).first()
            
            if not chave:
                return jsonify({'return': 'Not Exist'})
            else:
                if chave.status == 'Ok':
                    db.session.delete(chave)
                    db.session.commit()
                    return jsonify({'return':'Success', 'id': chave.id, 'status': chave.status})
                return jsonify({'return': 'Key not used', 'id': chave.id, 'status': chave.status})
        
    def deleteKeys():
        chaves = Chaves.query.filter_by(status='Ok')
        for chave in chaves:
            db.session.delete(chave)
            db.session.commit()
        return jsonify({'return':'Success'})

    ### COMPANIES ###

    @app.route(companies, methods=['GET'])
    def getCompanies():
        companies = Company.query.filter_by(status='Active')
        res = {}
        
        for company in companies:

            res[company.id] = {
                'id': company.id,
                'status': company.status
            }          
                
        return jsonify(res)

    @app.route(companies+'<id>', methods=['GET'])
    def getCompanyId(id):
        if isNull(id):
            return jsonify({'return':'Id is Null!'})

        company = Company.query.filter_by(id=str(id)).first()

        if not company:
            return jsonify({'return':'Company not exist!'})
        res = {
            'id': company.id,
            'status': company.status
        }

        return jsonify(res)

    @app.route(companies, methods=['POST'])
    def postCompany():
        id = request.form.get('id')

        if isNull(id):
            return jsonify({'return':'ID null!'})
        else:
            company = Company(str(id))
            db.session.add(company)
            db.session.commit()
            return jsonify({'id': company.id, 'status': company.status})

    @app.route(companies, methods=['PUT'])
    def putCompany():
        id = request.form.get('id')
        status = request.form.get('status')

        if isNull(id) or isNull(status):
            return jsonify({'return':'Values is Null'})

        company = Company.query.filter_by(id=str(id)).first()
        
        if not company:
            return jsonify({'return': 'Not Exist'})
        else:
            company.status = str(status)
            db.session.commit()
            company = Company.query.filter_by(id=str(id)).first()
            return jsonify({'id': company.id, 'status': company.status})

    @app.route(companies, methods=['DELETE'])
    def deleteCompany():
        id = request.form.get('id')

        if isNull(id): 
            return deleteCompanies()
        else:
            company = Company.query.filter_by(id=str(id)).first()
            
            if not company:
                return jsonify({'return': 'Not Exist'})
            else:
                if company.status == 'Inactive':
                    db.session.delete(company)
                    db.session.commit()
                    return jsonify({'return':'Success', 'id': company.id, 'status': company.status})
                return jsonify({'return': 'Key not used', 'id': company.id, 'status': company.status})
        
    def deleteCompanies():
        companies = Company.query.filter_by(status='Ok')
        for company in companies:
            db.session.delete(company)
            db.session.commit()
        return jsonify({'return':'Success'})

    ### Number Document ###

    @app.route(numberDocument, methods=['GET'])
    def getNumberDocuments():
        numberDocuments = NumberDocument.query.all()
        res = {}
        
        for numberDocument in numberDocuments:

            res[numberDocument.id] = {
                'id': numberDocument.id,
                'month': numberDocument.month,
                'status': numberDocument.status,
                'cnpj': numberDocument.cnpj
            }          
                
        return jsonify(res)

    @app.route(numberDocument+'<id>', methods=['GET'])
    def getNumberDocumentId(id):
        if isNull(id):
            return jsonify({'return':'Id is Null!'})

        numberDocument = NumberDocument.query.filter_by(id=str(id)).first()
        
        if not numberDocument:
            return jsonify({'return':'Number Document not exist!'})
        res = {
            'id': numberDocument.id,
            'month': numberDocument.month,
            'status': numberDocument.status,
            'cnpj': numberDocument.cnpj
        }

        return jsonify(res)

    @app.route(numberDocument, methods=['POST'])
    def postNumberDocument():
        id = request.form.get('id')
        month = request.form.get('month')
        status = request.form.get('status')
        cnpj = request.form.get('cnpj')

        if isNull(id) or isNull(month) or isNull(status) or isNull(cnpj):
            return jsonify({'return':'Values Null!'})
        else:
            isCnpj = Company.query.filter_by(id=str(cnpj)).first()

            if not isCnpj:
                company = Company(str(cnpj))
                db.session.add(company)
                db.session.commit()

            numberDocument = NumberDocument(str(id), str(month), str(status), str(cnpj))
            db.session.add(numberDocument)
            db.session.commit()
            res = {
                'id': numberDocument.id,
                'month': numberDocument.month,
                'status': numberDocument.status,
                'cnpj': numberDocument.cnpj
            }
            return jsonify(res)

    @app.route(numberDocument, methods=['PUT'])
    def putNumberDocument():
        id = request.form.get('id')
        month = request.form.get('month')
        status = request.form.get('status')
        cnpj = request.form.get('cnpj')

        if isNull(id):
            return jsonify({'return':'Id is Null!'})

        numberDocument = NumberDocument.query.filter_by(id=str(id)).first()
        
        if not numberDocument:
            return jsonify({'return': 'Not Exist'})
        else:
            if not isNull(month):
                numberDocument.month = month
            if not isNull(status):
                numberDocument.status = status
            if not isNull(cnpj):
                numberDocument.cnpj = cnpj
                
            db.session.commit()
            numberDocument = Company.query.filter_by(id=str(id)).first()
            
            res = {
                'id': numberDocument.id,
                'month': numberDocument.month,
                'status': numberDocument.status,
                'cnpj': numberDocument.cnpj
            }
            return jsonify(res)

    @app.route(numberDocument, methods=['DELETE'])
    def deleteNumberDocument():
        id = request.form.get('id')

        if isNull(id): 
            return jsonify({'return':'Ids Null!'})
        else:
            numberDocument = NumberDocument.query.filter_by(id=str(id)).first()
            
            if not numberDocument:
                return jsonify({'return': 'Not Exist'})
            else:
                if numberDocument.status == 'Inactive':
                    db.session.delete(numberDocument)
                    db.session.commit()

                    return jsonify({
                        'return':'Success', 
                        'id': numberDocument.id, 
                        'month': numberDocument.month,
                        'status': numberDocument.status,
                        'cnpj': numberDocument.cnpj
                    })

                return jsonify({
                    'return': 'Number Document is used', 
                    'id': numberDocument.id,
                    'month': numberDocument.month,
                    'status': numberDocument.status,
                    'cnpj': numberDocument.cnpj
                })
        
    def deleteCompanies():
        numberDocuments = NumberDocument.query.filter_by(status='Ok')
        for numberDocument in numberDocuments:
            db.session.delete(numberDocument)
            db.session.commit()
        return jsonify({'return':'Success'})

    def isNull(a):
        a = str(a)
        if not a or not a.strip() or a == 'None':
            return True
        return False

    
    return app