import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages')
from flask import Flask, jsonify, render_template, request
import nest
import os
import json
import anyjson
import helpers as hh


app = Flask(__name__)


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
    # import pdb;pdb.set_trace()
    nest.ResetKernel()

    with open('settings/simulation.json') as data_file:
        sims = anyjson.loads(''.join(data_file.readlines()))

    # nodes = nest.Models('nodes')
    with open('settings/models.json') as data_file:
        PARAMS = json.load(data_file)
    nodes = PARAMS.keys()
    nodes.sort()

    return render_template('multiple_neurons_mm.html', nodes=nodes, sims=sims, count=count)

@app.route('/parameters/', methods=['GET'])
def parameters():
    # import pdb;pdb.set_trace()
    model = request.values['model']
    preset = request.values.get('preset', 'default')

    with open('settings/models.json') as data_file:
        PARAMS = json.load(data_file)

    if model in PARAMS:
        params = dict(zip(PARAMS[model],nest.GetDefaults(model, PARAMS[model])))
    else:
        params = nest.GetDefaults(model)

    global recordables
    recordables = map( lambda x: x.name, nest.GetDefaults(model).get('recordables', []))

    presets_model = map(lambda x: os.path.splitext(x)[0], os.listdir('parameters'))
    presets = []
    if model in presets_model:
        with open('parameters/%s.json' %model) as data_file:
            data = json.load(data_file)
            presets = map(lambda x: x['label'], data)
            data = filter(lambda x: x['label']==preset, data)
            if data:
                params.update(data[0]['params'])

    return jsonify(params=params, presets=presets, recordables=recordables)

@app.route('/init/', methods=['POST'])
def init():
    # import pdb;pdb.set_trace()
    values = request.get_json()
    values['neuron']['params'] = dict(zip(values['neuron']['params'].keys(), map(float, values['neuron']['params'].values())))
    values['input']['params'] = dict(zip(values['input']['params'].keys(), map(float, values['input']['params'].values())))

    nest.ResetKernel()
    nest.SetKernelStatus({'rng_seeds': (int(values['kernel']['params']['rng_seeds']),)})

    global neuron
    neuron = nest.Create(values['neuron']['model'], values['neuron']['count'], params=values['neuron']['params'])

    global input
    input = nest.Create(values['input']['model'], params=values['input']['params'])
    nest.Connect(input,neuron, 'all_to_all')

    global mm
    mm = nest.Create('multimeter', params={"record_from": recordables})
    nest.Connect(mm,neuron, 'all_to_all')

    nest.Simulate(values.get('simtime', 500.))
    events = nest.GetStatus(mm,'events')[0]
    nest.SetStatus(mm, {'n_events': 0})

    return jsonify(data=dict([(x, hh.prep_multi(events, x)) for x in recordables]), values=values)

@app.route('/simulate/', methods=['POST'])
def simulate():
    values = request.get_json()
    values['input']['params'] = dict(zip(values['input']['params'].keys(), map(float, values['input']['params'].values())))
    values['neuron']['params'] = dict(zip(values['neuron']['params'].keys(), map(float, values['neuron']['params'].values())))

    nest.SetStatus(input, values['input']['params'])
    nest.SetStatus(neuron, values['neuron']['params'])
    nest.Simulate(1.)

    events = nest.GetStatus(mm,'events')[0]
    nest.SetStatus(mm, {'n_events': 0})

    return jsonify(data=dict([(x, hh.prep_multi(events, x)) for x in recordables]), values=values)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        app.run(sys.argv[1])
    else:
        app.run()
