import { Platform, View, StyleSheet } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import AppNavigator from './app/navigation/AppNavigator';
import { Colors } from './app/constants/colors';

export default function App() {
  if (Platform.OS === 'web') {
    return (
      <View style={styles.webContainer}>
        <View style={styles.phoneFrame}>
          <View style={styles.phoneScreen}>
            <StatusBar style="light" />
            <AppNavigator />
          </View>
        </View>
      </View>
    );
  }
  return (
    <>
      <StatusBar style="light" />
      <AppNavigator />
    </>
  );
}

const styles = StyleSheet.create({
  webContainer: {
    flex: 1,
    backgroundColor: '#06101A',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
  },
  phoneFrame: {
    width: 393,
    height: 852,
    backgroundColor: '#000000',
    borderRadius: 55,
    padding: 12,
    boxShadow: '0px 20px 80px rgba(0,194,168,0.15)',
  },
  phoneScreen: {
    flex: 1,
    backgroundColor: Colors.background,
    borderRadius: 44,
    overflow: 'hidden',
  },
});