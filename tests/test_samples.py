resolution_sample = {
    'status': 'ok', 
    'execution_time': '10ms',
    'resolutions': [
        { 
            'name': 'pipeline1',
            'status': 'failed',
            'steps': [
            { 
                'step_name': 'step1',
                'status' : 'ok', 
                'result': 10,
                'execution_time': '1ms'
            }, 
            {
                'step_name': 'step2', 
                'status' : 'failed', 
                'result': None, 
                'execution_time': '0.2ms'
                }
            ],
        },
    ]
}
