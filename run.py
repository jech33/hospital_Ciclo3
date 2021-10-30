from hospital import app

#Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

#prueba2