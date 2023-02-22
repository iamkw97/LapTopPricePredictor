from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)


def cost_prediction(input_list):
    file_name = 'model/laptop_price_model.pickle'
    with open(file_name, 'rb') as file:
        model = pickle.load(file)
    predicted_value = model.predict([input_list])
    return predicted_value


@app.route('/', methods=['POST', 'GET'])
def index():
    predicted_cost = 0

    if request.method == 'POST':
        cpu = request.form['cpu']
        clock_speed = request.form['clock_speed']
        ram = request.form['ram']
        storage = request.form['storage']
        gpu = request.form['gpu']
        os = request.form['os']
        company = request.form['company']
        category = request.form['category']
        screen_resolution = request.form['screen_resolution']
        weight = request.form['weight']
        warranty = request.form['warranty']
        touchscreen = request.form.getlist('touchscreen')
        ips = request.form.getlist('ips')

        # print(cpu, clock_speed, ram, storage, gpu, os, company, category,
        #       screen_resolution, weight, warranty, touchscreen, ips)

    # data list for each inputs
        cpu_list = ['i7', 'i5', 'i3', 'amd', 'other']
        clock_speed_list = ['3_', '2_3', '1_2', '_1']
        storage_list = ['128GB_SSD', '256GB_SSD', '512GB_SSD',
                        '1TB_SSD', '1TB_HDD', '1TB_HDD_128GB_SSD', '1TB_HDD_256GB_SSD']
        gpu_list = ['nvidia', 'intel', 'amd']
        os_list = ['windows', 'mac', 'linux', 'other']
        company_list = ['acer', 'apple', 'asus', 'dell',
                        'hp', 'lenovo', 'msi', 'toshiba', 'other']
        category_list = ['gaming', 'netbook', 'notebook',
                         'ultrabook', 'workstation', 'convertible']
        screen_resolution_list = [
            '1366x768', '1920x1080', '3200x1800', '3840x2160', 'other']
        warranty_list = ['1yrs', '1.6yrs', '2yrs', '3yrs']

    # conversion into an 2d array
        input_list = []

        def inputs_conversion(item):
            input_list.append(item)

        def selections_conversion(data, data_list):
            for i in data_list:
                if i == data:
                    input_list.append(1)
                else:
                    input_list.append(0)

        inputs_conversion(int(ram))
        inputs_conversion(float(weight))
        inputs_conversion(len(touchscreen))
        inputs_conversion(len(ips))
        selections_conversion(company, company_list)
        selections_conversion(category, category_list)
        selections_conversion(screen_resolution, screen_resolution_list)
        selections_conversion(storage, storage_list)
        selections_conversion(warranty, warranty_list)
        selections_conversion(cpu, cpu_list)
        selections_conversion(clock_speed, clock_speed_list)
        selections_conversion(gpu, gpu_list)
        selections_conversion(os, os_list)

    # get the cost of laptop
        predicted_cost = cost_prediction(input_list) * 389.06
        predicted_cost = np.round(predicted_cost[0])
        print(predicted_cost)

    return render_template("index.html", predicted_cost=predicted_cost)


if __name__ == '__main__':
    app.run(debug=True)
