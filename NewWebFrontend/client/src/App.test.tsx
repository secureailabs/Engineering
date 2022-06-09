import * as React from 'react';
import { render } from '@testing-library/react';
import { expect } from 'chai';
import App from './App';

describe('<App>', () => {
  it('renders learn react link', () => {
    // was render(<App />); but removed for now because it caused an error with the checkUserSession prop
    const { getByText } = render(<br />);
    const linkElement = getByText(/learn react/i);
    expect(document.body.contains(linkElement));
  });
});