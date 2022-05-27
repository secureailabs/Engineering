import React from 'react';

import {Navigate, useSearchParams} from 'react-router-dom';

const DevMode = () => {
    const [params] = useSearchParams();
    const mode = params.get("mode")

    if (mode) {
        localStorage.setItem('mode', mode == 'demo' ? 'demo' : 'prod')
        return <Navigate to={location.pathname.slice(0, location.pathname.indexOf('?'))} />
    }

    if (!localStorage.getItem("mode")) {
            localStorage.setItem("mode", "prod")
    }

    return <></>
}

export default DevMode;