from app import create_app, db

app = create_app()

@app.before_request
def create_data_dir():
    import os
    from app.config import Config
    os.makedirs(Config.BIOMETRIC_STORAGE, exist_ok=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)