import { useState } from 'react';
export const useTeam = () => {
    const [team, setTeam] = useState([]);
    return { team };
};
