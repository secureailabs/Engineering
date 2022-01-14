module.exports = {
  apps: [
    {
      name: 'SERVER',
      script: 'ts-node -r tsconfig-paths/register --files ./src/index.ts',
    },
  ],
};
