import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages')

from flask import Flask, jsonify, render_template, request, abort
import nest
import helpers as hh


app = Flask(__name__)

trusted_proxies = ('127.0.0.1','132.230.177.59')

@app.before_request
def limit_remote_addr():
    if request.remote_addr not in trusted_proxies:
        abort(403)  # Forbidden

@app.template_filter('stringify')
def stringify_filter(s):
    return s.replace('_',' ')

@app.route('/')
def init():
    # import pdb;pdb.set_trace()
    nest.ResetKernel()

    global neuron
    neuron = nest.Create('iaf_neuron', params={'C_m': 250., 'tau_m': 10.})

    global input
    input = nest.Create('noise_generator', params={'mean':250., 'std':250.})
    nest.Connect(input,neuron)

    global vm
    vm = nest.Create('voltmeter')
    nest.Connect(vm,neuron)

    nest.Simulate(1000.)
    events = nest.GetStatus(vm,'events')[0]
    nest.SetStatus(vm, {'n_events': 0})

    # return render_template('iaf_neuron.html', data=hh.prep_single([events['times'], events['V_m']]))
    return render_template('iaf_neuron_jquery-slider.html', data=hh.prep_single([events['times'], events['V_m']]))


@app.route('/simulate/', methods=['POST'])
def simulate():

    values = request.get_json()
    nest.SetStatus(input, {'mean':float(values['mean']),'std':float(values['std'])})
    nest.SetStatus(neuron, {'C_m':float(values['C_m']),'tau_m':float(values['tau_m'])})

    nest.Simulate(1.)
    events = nest.GetStatus(vm,'events')[0]
    nest.SetStatus(vm, {'n_events': 0})

    return jsonify(data=hh.prep_single([events['times'], events['V_m']]))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        app.run(sys.argv[1])
    else:
        app.run()
