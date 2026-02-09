import { motion } from 'framer-motion';

const EntityNetworkCard = ({ data, loading }) => {
    if (loading) {
        return (
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 h-full">
                <div className="animate-pulse space-y-3">
                    <div className="h-8 bg-white/20 rounded w-1/3 mb-4"></div>
                    <div className="h-40 bg-white/20 rounded"></div>
                </div>
            </div>
        );
    }

    const entities = data?.entities || {};
    const relationships = data?.relationships || {};
    const mostMentioned = data?.most_mentioned || {};

    const tasks = entities.tasks || [];
    const people = entities.people || [];
    const technologies = entities.technologies || [];

    const topTasks = mostMentioned.tasks || [];
    const topPeople = mostMentioned.people || [];
    const topTech = mostMentioned.technologies || [];

    const getTechCategory = (tech) => {
        const categories = {
            languages: '💻',
            frameworks: '🔧',
            databases: '🗄️',
            cloud: '☁️',
            tools: '🛠️'
        };
        return categories[tech.category] || '⚙️';
    };

    return (
        <motion.div
            whileHover={{ scale: 1.01 }}
            className="bg-gradient-to-br from-cyan-900/40 to-blue-900/40 backdrop-blur-md rounded-2xl p-6 border border-cyan-500/30 shadow-xl shadow-cyan-500/20 h-full flex flex-col"
        >
            {/* Header */}
            <div className="mb-6">
                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                    <span className="text-3xl">🔗</span>
                    Entity Network
                </h2>
                <p className="text-cyan-300 text-sm mt-1">People, Tasks & Technologies</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-3 gap-3 mb-6">
                <div className="bg-white/10 rounded-xl p-3 border border-white/20 text-center">
                    <div className="text-2xl mb-1">👥</div>
                    <div className="text-white font-bold text-xl">{people.length}</div>
                    <div className="text-cyan-300 text-xs">People</div>
                </div>
                <div className="bg-white/10 rounded-xl p-3 border border-white/20 text-center">
                    <div className="text-2xl mb-1">📋</div>
                    <div className="text-white font-bold text-xl">{tasks.length}</div>
                    <div className="text-cyan-300 text-xs">Tasks</div>
                </div>
                <div className="bg-white/10 rounded-xl p-3 border border-white/20 text-center">
                    <div className="text-2xl mb-1">⚙️</div>
                    <div className="text-white font-bold text-xl">{technologies.length}</div>
                    <div className="text-cyan-300 text-xs">Tech</div>
                </div>
            </div>

            {/* Relationships Summary */}
            <div className="mb-4 bg-white/10 rounded-xl p-3 border border-white/20">
                <div className="text-cyan-300 text-xs font-semibold mb-2">Relationships</div>
                <div className="grid grid-cols-2 gap-2 text-xs">
                    <div className="text-white">
                        👥→📋 {relationships.person_task?.length || 0}
                    </div>
                    <div className="text-white">
                        👥→⚙️ {relationships.person_technology?.length || 0}
                    </div>
                    <div className="text-white">
                        👥→👥 {relationships.person_person?.length || 0}
                    </div>
                    <div className="text-white">
                        📋→⚙️ {relationships.task_technology?.length || 0}
                    </div>
                </div>
            </div>

            {/* Most Mentioned Entities */}
            <div className="flex-1 overflow-y-auto custom-scrollbar space-y-4">
                {/* Top Tasks */}
                {topTasks.length > 0 && (
                    <div>
                        <div className="text-cyan-300 text-sm font-semibold mb-2 flex items-center gap-2">
                            <span>📋</span>
                            Most Mentioned Tasks
                        </div>
                        <div className="space-y-2">
                            {topTasks.slice(0, 5).map(([task, count], idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: idx * 0.05 }}
                                    className="bg-white/10 rounded-lg p-2 border border-white/20 flex items-center justify-between"
                                >
                                    <span className="text-white text-sm font-mono">{task}</span>
                                    <span className="px-2 py-1 bg-cyan-500/20 text-cyan-300 rounded-full text-xs">
                                        {count}x
                                    </span>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Top Technologies */}
                {topTech.length > 0 && (
                    <div>
                        <div className="text-cyan-300 text-sm font-semibold mb-2 flex items-center gap-2">
                            <span>⚙️</span>
                            Most Discussed Tech
                        </div>
                        <div className="flex flex-wrap gap-2">
                            {topTech.slice(0, 8).map(([tech, count], idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, scale: 0.8 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    transition={{ delay: idx * 0.05 }}
                                    className="px-3 py-1 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 rounded-full flex items-center gap-2"
                                >
                                    <span className="text-white text-sm">{tech}</span>
                                    <span className="text-cyan-300 text-xs font-bold">{count}</span>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Top People */}
                {topPeople.length > 0 && (
                    <div>
                        <div className="text-cyan-300 text-sm font-semibold mb-2 flex items-center gap-2">
                            <span>👥</span>
                            Most Active People
                        </div>
                        <div className="space-y-2">
                            {topPeople.slice(0, 5).map(([person, count], idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: idx * 0.05 }}
                                    className="bg-white/10 rounded-lg p-2 border border-white/20 flex items-center justify-between"
                                >
                                    <span className="text-white text-sm">{person}</span>
                                    <span className="px-2 py-1 bg-cyan-500/20 text-cyan-300 rounded-full text-xs">
                                        {count} mentions
                                    </span>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Empty State */}
                {topTasks.length === 0 && topTech.length === 0 && topPeople.length === 0 && (
                    <div className="text-center text-cyan-300 py-8">
                        <div className="text-4xl mb-2">🔍</div>
                        <div>No entities detected yet</div>
                    </div>
                )}
            </div>
        </motion.div>
    );
};

export default EntityNetworkCard;
