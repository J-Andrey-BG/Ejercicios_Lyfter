class Printer:

    def print_document(self, document):
        print(f"Printing document: {document}")


class Scanner:

    def scan_document(self, document):
        print(f"Scanning document: {document}")


class MultiFunctionDevice(Printer, Scanner):

    def copy_document(self, document):
        self.scan_document(document)
        self.print_document(document)