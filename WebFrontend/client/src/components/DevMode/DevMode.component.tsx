import React from 'react';

import {Navigate, useSearchParams} from 'react-router-dom';

const DevMode = () => {
    const [params] = useSearchParams();
    const mode = params.get("mode")

    if(mode =="demo"){
        localStorage.setItem("mode", "demo")
    } else {
        if (!localStorage.getItem("mode")) {
            localStorage.setItem("mode", "prod")
        }
    }
    
    if (mode) {
        return <Navigate to={location.pathname.slice(0, location.pathname.indexOf('?'))} />
    }
    return <></>
}

export default DevMode;