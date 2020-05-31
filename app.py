from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def zoeken():
    if request.method == "POST":
        zoeken = request.form.get("zoek", "")
        rows = database(zoeken)

        return render_template("afvink3.html", database=rows, zoek=zoeken)

    else:
        rows = database("None")
        return render_template("afvink3.html", database=rows,
                               zoek="None")


def database(zoek):
    """ haalt de description uit de ensembldb database
     en filtert deze op het zoekwoord

    :param zoek: Het ingegeven zoekwoord
    :return: Een lijst met de juiste discriptions
    """
    print("zoek woord is:", zoek)
    conn = mysql.connector.connect(host='ensembldb.ensembl.org',
                                   user='anonymous',
                                   db='homo_sapiens_core_95_38')
    cursor = conn.cursor()
    cursor.execute("select description from gene")
    rows = cursor.fetchall()
    des = []
    for row in rows:
        if str(row) != "(None,)":
            if zoek.upper() in str(row).upper() or zoek is 'None':
                des.append(row)

    cursor.close()
    conn.close()
    return des


if __name__ == '__main__':
    app.run()