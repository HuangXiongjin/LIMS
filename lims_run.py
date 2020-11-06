from lims_backend import manager, app


def main():
    app.run(port=10002)
    # manager.run()


if __name__ == '__main__':
    main()
