from epi_creator import create_app

app = create_app()


if __name__ == "__main__":
    # print("runnn")
    app.run(debug=True, host="0.0.0.0", port=5005)
