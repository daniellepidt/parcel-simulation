// Conveniently import this file anywhere to use db

import firebase from 'firebase/app'
import 'firebase/firestore'

export const db = firebase
    .initializeApp({ projectId: 'menny-s-parcel-simulator' })
    .firestore()


// Export types that exists in Firestore - Uncomment if you need them in your app
// const { Timestamp, GeoPoint } = firebase.firestore
// export { Timestamp, GeoPoint }

db.settings({ timestampsInSnapshots: true })