const downloadFileText = (content:string, name:string):void => {
    const element = document.createElement("a")
    const file = new Blob([content], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = name;
    document.body.appendChild(element);
    element.click();
}

export default downloadFileText;