import { createSlice } from '@reduxjs/toolkit';

const projectSlice = createSlice({
    name: 'projects',
    initialState: { list: [], loading: false },
    reducers: {
        setProjects: (state, action) => {
            state.list = action.payload;
        },
    },
});

export const { setProjects } = projectSlice.actions;
export default projectSlice.reducer;
