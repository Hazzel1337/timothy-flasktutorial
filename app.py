from website import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) #always restarts the webs server after changes
