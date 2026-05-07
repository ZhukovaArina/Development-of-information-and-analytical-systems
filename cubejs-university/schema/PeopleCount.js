cube(`PeopleCount`, {
  sql: `SELECT * FROM uni.people_count`,

  measures: {
    total_people: {
      sql: `people_count`,
      type: `sum`,
      title: `Всего людей`
    }
  },

  dimensions: {
    window_start: {
      sql: `window_start`,
      type: `time`,
      title: `Начало окна`
    },
    building_id: {
      sql: `building_id`,
      type: `number`,
      title: `Корпус`
    }
  }
});
