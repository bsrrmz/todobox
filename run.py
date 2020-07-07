from App import createApp, db

app = createApp()

# create the database and the database tables
db.create_all(app=app)

if __name__=='__main__':
    app.run(debug=True)