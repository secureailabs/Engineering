import React from 'react';

import Customizabledashboard from './CustomizableDashboard.component';
import { useQueryClient } from 'react-query';

const CustomizableDashboardContainer: React.FC = () => {
  
  // @ts-ignore
  return Customizabledashboard({userData: useQueryClient().getQueryData('userData') })
}

export default CustomizableDashboardContainer
