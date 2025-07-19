from app import create_app, db

app = create_app()

@app.cli.command()
def init_db():
    """Create database tables."""
    db.create_all()
    print('Database tables created.')

@app.cli.command()
def seed_db():
    """Seed database with sample data."""
    from seed_data import create_sample_data
    create_sample_data()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
