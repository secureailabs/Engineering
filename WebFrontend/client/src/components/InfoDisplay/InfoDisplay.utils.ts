import _ from 'lodash';

export const removeValues = (
  object: Record<string, any>,
  keys: Array<string>
) => {
  for (const key of keys) {
    if (object[key]) {
      delete object[key];
    }
  }
  return object;
};

export const convertObjectToArray = (obj: Record<string, any>) => {
  return Object.entries(obj).map(([key, value]) => [key, value]);
};

export const reorganizeObject = (
  obj: Record<string, any>,
  order: Array<string>
) => {
  var newObject: Record<string, any> = {};
  for (var i = 0; i < order.length; i++) {
    if (obj.hasOwnProperty(order[i])) {
      newObject[order[i]] = obj[order[i]];
    }
  }
  return newObject;
};

export const reorganizeArray = (
  array: Array<Array<any>>,
  order: Array<string>
) => {
  var newArray: Array<Array<any>> = [];
  for (var i = 0; i < order.length; i++) {
    const value = _.find(array, function (o) {
      // console.log(o[0]);
      // console.log('ORDER I: ', order[i]);
      return o[0] === order[i];
    });
    //@ts-ignore
    newArray[i] = [order[i], value[1]];
  }

  return newArray;
};

export const changeArrayKeys = (
  array: Array<Array<any>>,
  newKeys: Array<string>
) => {
  for (var i = 0; i < newKeys.length; i++) {
    array[i][0] = newKeys[i];
  }
  return array;
}
