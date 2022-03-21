export interface IDefaults {
    error: {
      error: {
        response: {
          data: {
            response: string,
            message: string
          }
        }
      }
    } | null;
    errorMessage: {
      response: string,
      message: string
    } | null;
    state: 'isLoading' | 'success' | 'failure' | null;
    reset(): void;
  }