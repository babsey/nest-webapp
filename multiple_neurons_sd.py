from flask import Flask, jsonify, render_template, request
import numpy as np
import nest
import os
import json
import anyjson

app = Flask(__name__)

def prep(data):
    return map(lambda x: {'x':x[0], 'y':x[1]},  zip(*data))

@app.template_filter('neurons')
def neurons_filter(nodes):
    return filter(lambda node: 'generator' not in node, nodes)

@app.template_filter('inputs')
def inputs_filter(nodes):
    return filter(lambda node: 'generator' in node, nodes)


@app.template_filter('stringify')
def stringify_filter(s):
    return s.replace('_',' ')

@app.route('/')
@app.route('/<count>')
def main(count=1):
    nest.ResetKernel()

    with open('settings/simulation.json') as data_file:
        sims = anyjson.loads(''.join(data_file.readlines()))

    # nodes = nest.Models('nodes')
    with open('settings/models.json') as data_file:
        PARAMS = json.load(data_file)
    nodes = PARAMS.keys()

    return render_template('multiple_neurons_sd.html', nodes=nodes, sims=sims, count=count)

@app.route('/parameters/', methods=['GET'])
def parameters():
    model = request.values['model']
    preset = request.values.get('preset', 'default')

    with open('settings/models.json') as data_file:
        PARAMS = json.load(data_file)

    if model in PARAMS:
        params = dict(zip(PARAMS[model],nest.GetDefaults(model, PARAMS[model])))
    else:
        params = nest.GetDefaults(model)

    presets_model = map(lambda x: os.path.splitext(x)[0], os.listdir('parameters'))
    presets = []
    if model in presets_model:
        with open('parameters/%s.json' %model) as data_file:
            data = json.load(data_file)
            presets = map(lambda x: x['label'], data)
            data = filter(lambda x: x['label']==preset, data)
            if data:
                params.update(data[0]['params'])

    return jsonify(params=params, presets=presets)

@app.route('/init/', methods=['POST'])
def init():
    values = request.get_json()
    values['neuron']['params'] = dict(zip(values['neuron']['params'].keys(), map(lambda x: float(x), values['neuron']['params'].values())))
    values['input']['params'] = dict(zip(values['input']['params'].keys(), map(lambda x: float(x), values['input']['params'].values())))

    nest.ResetKernel()


    global neuron
    neuron = nest.Create(values['neuron']['model'], values['neuron']['count'], params=values['neuron']['params'])

    global input
    input = nest.Create(values['input']['model'], params=values['input']['params'])
    nest.Connect(input, neuron, 'all_to_all')

    global sd
    sd = nest.Create('spike_detector')
    nest.Connect(neuron, sd, 'all_to_all')

    nest.Simulate(1000.)
    events = nest.GetStatus(sd,'events')[0]
    nest.SetStatus(sd, {'n_events': 0})
    if events:
        data = prep([events['times'],events['senders']])
    else:
        data = []

    return jsonify(data=prep([events['times'],events['senders']]), values=values, curtime=nest.GetStatus([0],'time'))

@app.route('/simulate/', methods=['POST'])
def simulate():
    values = request.get_json()
    values['input']['params'] = dict(zip(values['input']['params'].keys(), map(lambda x: float(x), values['input']['params'].values())))
    values['neuron']['params'] = dict(zip(values['neuron']['params'].keys(), map(lambda x: float(x), values['neuron']['params'].values())))

    nest.SetStatus(input, values['input']['params'])
    nest.SetStatus(neuron, values['neuron']['params'])
    nest.Simulate(1.)

    events = nest.GetStatus(sd,'events')[0]
    nest.SetStatus(sd, {'n_events': 0})
    if events:
        data = prep([events['times'],events['senders']])
    else:
        data = []

    return jsonify(data=prep([events['times'],events['senders']]), values=values, curtime=nest.GetStatus([0],'time'))

if __name__ == '__main__':
    app.run()
