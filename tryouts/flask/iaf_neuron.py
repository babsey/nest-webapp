from flask import Flask, jsonify, render_template, request
import nest

app = Flask(__name__)

def prep(data):
    data_zipped = zip(*data)
    return map(lambda x: {'x':x[0], 'y':x[1]}, data_zipped)

@app.template_filter('stringify')
def stringify_filter(s):
    return s.replace('_',' ')

@app.route('/')
def init():
    nest.ResetKernel()

    global neuron
    neuron = nest.Create('iaf_neuron')

    global input
    input = nest.Create('noise_generator', params={'mean':300., 'std':300.})
    nest.Connect(input,neuron)

    global vm
    vm = nest.Create('voltmeter')
    nest.Connect(vm,iaf)

    nest.Simulate(1000)
    vm_E = nest.GetStatus(vm,'events')[0]
    nest.SetStatus(vm, {'n_events': 0})


    return render_template('iaf_neuron.html', data=prep([vm_E['times'], vm_E['V_m']]), nodes=nodes)


@app.route('/simulate/', methods=['GET'])
def simulate():
    nest.SetStatus(ng, {'mean':float(request.values['mean']),'std':float(request.values['std'])})
    nest.SetStatus(iaf, {'C_m':float(request.values['C_m']),'tau_m':float(request.values['tau_m'])})
    nest.Simulate(1)
    vm_E = nest.GetStatus(vm,'events')[0]
    nest.SetStatus(vm, {'n_events': 0})
    return jsonify(data=prep([vm_E['times'], vm_E['V_m']]))

if __name__ == '__main__':
    app.run()
