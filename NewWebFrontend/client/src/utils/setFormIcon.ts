import type { FormState } from 'react-hook-form';

const setFormIcon = (
  formState: FormState<any>,
  field: string,
  controlled = false,
  defaultHidden = false,
  showSuccess = true,
  isOnSubmit = false,
): string | undefined => {
  const dirty = formState.dirtyFields[field];
  const touched = formState.touchedFields[field];
  const error = formState.errors[field];
  console.log(`setFormIcon: ${field}`)
  console.log(formState)
  console.log(dirty)
  console.log(touched)
  console.log(error)
  
  // Update field icon
  if (dirty && (controlled || touched) && !error) {
    return showSuccess ? 'V' : (!defaultHidden ? '?' : undefined);
  } else if ((touched || (dirty && controlled) || isOnSubmit) && error) {
    return 'X';
  } else {
    return !defaultHidden ? '?' : undefined;
  }
};

export default setFormIcon;
