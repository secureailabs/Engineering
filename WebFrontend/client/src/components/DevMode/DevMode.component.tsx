import React from 'react';

import {Navigate, useSearchParams} from 'react-router-dom';

const DevMode = () => {
    const [params] = useSearchParams();
    const mode = params.get("mode")
    if(mode =="demo"){
        localStorage.setItem("mode", "demo")
    } else {
        localStorage.setItem("mode", "prod")
    }
    return (
        <Navigate to="/login" />
    )
}

export default DevMode;