import React from "react";
import { QueryStatus } from "react-query";

type TConditionalRender = {
    status: QueryStatus,
    error: () => React.ReactElement,
    success: (data: any) => React.ReactElement,
    children:  React.ReactElement

}

export default TConditionalRender