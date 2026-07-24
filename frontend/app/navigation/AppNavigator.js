import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Colors } from '../constants/colors';

import HomeScreen from '../screens/HomeScreen';
import TripSetupScreen from '../screens/TripSetupScreen';
import VoteScreen from '../screens/VoteScreen';
import MembersScreen from '../screens/MembersScreen';
import ResultsScreen from '../screens/ResultsScreen';

const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerStyle: { backgroundColor: Colors.background },
          headerTintColor: Colors.accent,
          headerTitleStyle: {
            fontWeight: '600',
            color: Colors.textPrimary,
          },
          contentStyle: { backgroundColor: Colors.background },
          headerShadowVisible: false,
        }}
      >
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="TripSetup"
          component={TripSetupScreen}
          options={{ title: 'New Trip' }}
        />
        <Stack.Screen
          name="Vote"
          component={VoteScreen}
          options={{ title: 'Join a Trip' }}
        />
        <Stack.Screen
          name="Members"
          component={MembersScreen}
          options={{ title: 'Trip Members' }}
        />
        <Stack.Screen
          name="Results"
          component={ResultsScreen}
          options={{ title: 'Flight Options' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}