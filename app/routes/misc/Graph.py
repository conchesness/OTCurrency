from .BarGraph import Bar
from app.routes.Classes import Transaction


def graph():
    bar = Bar()

    x = [x.category for x in Transaction.objects()]
    x = set(x)
    x = list(x)
    values = []

    for i in x:

        values.append(len(Transaction.objects(category=i)))

    bar.setaxis(x, values)

    bar.graph()
