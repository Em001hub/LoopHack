import { useState, useEffect } from 'react';
import projectService from '../services/project.service';

export const useProjects = () => {
    const [projects, setProjects] = useState([]);
    useEffect(() => {
        projectService.getAll().then(setProjects);
    }, []);
    return { projects };
};
