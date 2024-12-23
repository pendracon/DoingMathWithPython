import matplotlib.pyplot as plt

import weather.db.weatherdb as db
from weather.model.service_error import NoError

def PlotHourlyData(config, conn, hours, data, data_type_id, savePath = None):
    serr = NoError
    data_type = None

    if conn:
        data_type, serr = db.get_datatype(config, conn, data_type_id)

    if not serr.IsError():
        x_1 = hours[0]
        x_2 = hours[len(hours)-1]
        y_1 = sorted(data)[0]
        y_2 = sorted(data)[len(data)-1]

        plt.plot(hours, data, marker='o')
        plt.xlabel('Hour')
        plt.ylabel(data_type_id.lower())
        plt.title(f'{data_type.get(mdl.KEY_DESC)} in NYC')
        plt.axis([x_1, x_2, y_1, y_2])
        plt.xticks(range(x_1, x_2))
        #plt.yticks(range(0, 101, 10))  # Add markers on the y-axis
        plt.grid(which='both', axis='both', linestyle=':', linewidth=0.5)  # Optional: light grid lines for reference

        if savePath:
            plt.savefig(savePath + f'/{data_type_id.lower()}_hourly.png')  # Save the plot to a file
        else:
            plt.show()

    return serr
# end def: PlotHourlyData
