cube(`StudentFeatures`, {
  sql: `SELECT * FROM uni.student_features`,

  measures: {
    count: {
      sql: `student_id`,
      type: `count`,
      title: `Студентов`
    },
    avg_score: {
      sql: `avg_score`,
      type: `avg`,
      title: `Средний балл`
    }
  },

  dimensions: {
    performance_level: {
      sql: `performance_level`,
      type: `string`,
      title: `Уровень`
    }
  }
});
