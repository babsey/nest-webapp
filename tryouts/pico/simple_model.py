import json
import nest

global vm

def init():
    nest.ResetKernel()
    iaf = nest.Create('iaf_neuron')
    ng = nest.Create('noise_generator')
    nest.Connect(ng,iaf)

    vm = nest.Create('voltmeter')

    nest.Connect(vm,iaf)


def run():
    nest.Simulate(10)
    Vm_E = nest.GetStatus(vm,'events')[0]
    return json.dumps(Vm_E)


init()
run()
