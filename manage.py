from equipment_backend import manager, app


def main():
    app.run('0.0.0.0', 5001)
    # manager.run()


if __name__ == '__main__':
    main()
